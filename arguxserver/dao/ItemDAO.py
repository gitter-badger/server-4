"""Data Access Object class for handling Items."""

from arguxserver.models import (
    ItemCategory,
    ItemName,
    ItemType,
    Item,
    TriggerSeverity
)

from arguxserver.dao.util import (
    VALUE_CLASS,
    TRIGGER_CLASS,
    ALERT_CLASS
)

from sqlalchemy.orm import joinedload


class ItemDAO:

    """
    Item DAO.
    """

    def __init__(self, session):
        """Initialise ItemDAO."""
        self.db_session = session

    def get_items_from_host(self, host):
        """Get all items registered on a host."""
        item = self.db_session.query(Item)\
            .options(joinedload('name'))\
            .filter(Item.host_id == host.id)
        return item

    def get_item_count_from_host(self, host):
        """Get number of items registered on a host."""
        n_items = self.db_session.query(Item)\
            .filter(Item.host_id == host.id)\
            .count()
        return n_items

    def get_item_by_host_key(self, host, key):
        """Get item registered on a host."""
        item = self.db_session.query(Item)\
            .options(joinedload(Item.name))\
            .filter(Item.host_id == host.id)\
            .filter(Item.key == key).first()
        return item

    def create_item(self, properties):
        """Create new Item."""
        item = Item(
            host_id=properties['host'].id,
            name=properties['name'],
            key=properties['key'],
            category=properties['category'],
            itemtype=properties['itemtype'])

        self.db_session.add(item)
        return item

    def create_trigger(self, item, name, rule, description="", severity="info"):
        """Create trigger."""
        trigger_klass = TRIGGER_CLASS.get(item.itemtype.name)

        severity = self.db_session.query(TriggerSeverity)\
            .filter(TriggerSeverity.key == severity).first()

        if not severity:
            raise ValueError('Severity "'+severity+'" is invalid')

        if not trigger_klass.validate_rule(rule):
            raise ValueError('Rule "'+rule+'" can\'t be validated')

        trigger = trigger_klass(name=name,
                                rule=rule,
                                description=description,
                                item_id=item.id,
                                severity_id=severity.id)
        self.db_session.add(trigger)
        return trigger

    def evaluate_trigger(self, trigger):
        """Evaluate Trigger."""
        item = trigger.item

        alert_klass = ALERT_CLASS.get(item.itemtype.name)

        i = trigger.validate_rule(trigger.rule)
        if i is None:
            return False

        handler = trigger.trigger_handlers.get(i[0], None)

        if handler:
            alert = self.db_session.query(alert_klass)\
                .filter(alert_klass.trigger_id == trigger.id)\
                .filter(alert_klass.end_time.is_(None)).first()

            (is_active, time) = handler(trigger, self.db_session, i[1], i[2], i[3])

            if is_active:
                if not alert:
                    trigger.active_alert = True
                    alert = alert_klass(trigger_id=trigger.id,
                                        start_time=time,
                                        end_time=None)
                    self.db_session.add(alert)
            else:
                if alert:
                    trigger.active_alert = False
                    alert.end_time = time
        else:
            print("Handler not found")
            return False

    def validate_trigger_rule(self, item, rule):
        """Return True if Trigger-rule is valid."""
        trigger_klass = TRIGGER_CLASS.get(item.itemtype.name)

        ret = trigger_klass.validate_rule(rule)
        if ret is None:
            return False

        return True

    def get_triggers(self, item):
        """Return all triggers on an item."""
        trigger_klass = TRIGGER_CLASS.get(item.itemtype.name)
        triggers = self.db_session.query(trigger_klass)\
            .options(joinedload(trigger_klass.item).joinedload(Item.name))\
            .filter(trigger_klass.item_id == item.id)

        return triggers

    def get_all_triggers(self):
        """Return all triggers."""
        triggers = []
        for name in TRIGGER_CLASS:
            klass = TRIGGER_CLASS[name]
            triggers.extend(self.db_session.query(klass).all())

        return triggers

    def get_last_alert_for_trigger(self, trigger):
        """Return last alert for a trigger.

        This function is used for every trigger individually...
        It makes more sense if we could query it for all triggers at once.
        """
        alert_klass = ALERT_CLASS.get(trigger.item.itemtype.name)

        alert = self.db_session.query(alert_klass)\
            .filter(alert_klass.trigger_id == trigger.id)\
            .order_by(alert_klass.start_time.desc())\
            .first()

        return alert

    def push_value(self, item, timestamp, value):
        """Push new value to an item."""
        value_klass = VALUE_CLASS.get(item.itemtype.name, None)

        val = value_klass(item_id=item.id, timestamp=timestamp, value=value)
        self.db_session.add(val)
        return val

    def get_last_value(self, item):
        """Return last value published on an item."""
        klass = VALUE_CLASS.get(item.itemtype.name, lambda: "nothing")

        val = self.db_session.query(klass)\
            .filter(klass.item_id == item.id)\
            .order_by(klass.timestamp.desc())\
            .first()

        return val

    # pylint: disable=unused-argument
    def get_values(self, item, start_time=None, end_time=None, count=-1):
        """Query values."""
        klass = VALUE_CLASS.get(item.itemtype.name, "nothing")

        query = self.db_session.query(klass)\
            .filter(klass.item_id == item.id)

        if start_time:
            query = query.filter(
                klass.timestamp > start_time)

        if end_time:
            query = query.filter(
                klass.timestamp < end_time)

        values = query.order_by(klass.timestamp.asc()).all()

        return values

    def get_alerts(self, item, active=True, inactive=False):
        """Query Alerts."""
        alert_klass = ALERT_CLASS.get(item.itemtype.name)
        alerts = []
        triggers = self.get_triggers(item)

        for trigger in triggers:
            active_alert = self.db_session.query(alert_klass)\
                .filter(alert_klass.trigger_id == trigger.id)\
                .filter(alert_klass.end_time.is_(None))

            alerts.extend(active_alert)

        return alerts

    def get_active_alert_count(self, item):
        """Get number of active alerts."""
        alert_klass = ALERT_CLASS.get(item.itemtype.name)
        triggers = self.get_triggers(item)

        n_alerts = 0

        for trigger in triggers:
            n_alerts += self.db_session.query(alert_klass)\
                .filter(alert_klass.trigger_id == trigger.id)\
                .filter(alert_klass.end_time.is_(None))\
                .count()

        return n_alerts

    def get_itemname_by_name(self, name):
        item_name = self.db_session.query(ItemName)\
            .filter(ItemName.name == name)\
            .first()

        return item_name

    def create_itemname(self, name, description):
        item_name = ItemName(name=name, description=description)
        self.db_session.add(item_name)
        return item_name

    def get_itemcategory_by_name(self, name):
        cat = self.db_session.query(ItemCategory)\
            .filter(ItemCategory.name == name).first()
        return cat

    def create_itemcategory(self, name):
        cat = ItemCategory(name=name)
        self.db_session.add(cat)
        return cat

    def get_itemtype_by_name(self, name):
        item_type = self.db_session.query(ItemType)\
            .filter(ItemType.name == name).first()
        return item_type

    def delete_trigger_by_id(self, item, trigger_id):
        """Delete Trigger for Item."""
        trigger_klass = TRIGGER_CLASS.get(item.itemtype.name)

        trigger = self.db_session.query(trigger_klass)\
            .filter(trigger_klass.id == trigger_id)\
            .filter(trigger_klass.item_id == item.id)\
            .first()

        if trigger:
            self.db_session.query(trigger_klass)\
                .filter(trigger_klass.id == trigger_id)\
                .filter(trigger_klass.item_id == item.id)\
                .delete()
        else:
            raise ValueError("trigger_id not valid for item")

        return
