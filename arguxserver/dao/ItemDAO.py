"""Data Access Object class for handling Items."""

from arguxserver.models import (
    DB_SESSION,
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

from sqlalchemy.orm import (
    sessionmaker
)


def get_items_from_host(host):
    """Get all items registered on a host."""
    item = DB_SESSION.query(Item).filter(Item.host_id == host.id)
    return item


def get_item_by_host_key(host, key):
    """Get item registered on a host."""
    item = DB_SESSION.query(Item)\
        .filter(Item.host_id == host.id)\
        .filter(Item.key == key).first()
    return item


def create_item(host, key, name, category, itemtype):
    """Create new Item."""
    item = Item(host_id=host.id, key=key, name=name, category=category, itemtype=itemtype)
    DB_SESSION.add(item)
    return item


def create_trigger(item, name, rule, description="", severity="info"):
    """Create trigger."""
    trigger_klass = TRIGGER_CLASS.get(item.itemtype.name)

    severity = DB_SESSION.query(TriggerSeverity)\
        .filter(TriggerSeverity.key == severity).first()

    if not severity:
        raise Exception()

    if not trigger_klass.validate_rule(rule):
        raise Exception()

    trigger = trigger_klass(name=name,
                            rule=rule,
                            description=description,
                            item_id=item.id,
                            severity_id=severity.id)
    DB_SESSION.add(trigger)
    return trigger


def evaluate_trigger(trigger):
    """Evaluate Trigger."""
    item = trigger.item

    alert_klass = ALERT_CLASS.get(item.itemtype.name)

    Session = sessionmaker()
    session = Session()

    i = trigger.validate_rule(trigger.rule)
    if i is None:
        return False

    handler = trigger.trigger_handlers.get(i[0], None)

    if handler:
        alert = session.query(alert_klass)\
            .filter(alert_klass.trigger_id == trigger.id)\
            .filter(alert_klass.end_time is None).first()

        (is_active, time) = handler(trigger, session, i[1], i[2], i[3])

        if is_active:
            if not alert:
                alert = alert_klass(trigger_id=trigger.id,
                                    start_time=time,
                                    end_time=None)
                session.add(alert)
                session.commit()
        else:
            if alert:
                alert.end_time = time
                session.commit()
        session.close()
    else:
        session.close()
        return False


def get_triggers(item):
    """Return all triggers on an item."""
    trigger_klass = TRIGGER_CLASS.get(item.itemtype.name)
    triggers = DB_SESSION.query(trigger_klass)\
        .filter(trigger_klass.item_id == item.id)

    return triggers


def get_all_triggers():
    """Return all triggers."""
    triggers = []
    for name in TRIGGER_CLASS:
        klass = TRIGGER_CLASS[name]
        triggers.extend(DB_SESSION.query(klass).all())

    return triggers


def push_value(item, timestamp, value):
    """Push new value to an item."""
    value_klass = VALUE_CLASS.get(item.itemtype.name, None)

    val = value_klass(item_id=item.id, timestamp=timestamp, value=value)
    DB_SESSION.add(val)
    return val


def get_last_value(item):
    """Return last value published on an item."""
    klass = VALUE_CLASS.get(item.itemtype.name, lambda: "nothing")

    val = DB_SESSION.query(klass)\
        .filter(klass.item_id == item.id)\
        .order_by(klass.timestamp.desc())\
        .first()

    return val


# pylint: disable=unused-argument
def get_values(item, start_time=None, end_time=None, count=-1):
    """Query values."""
    klass = VALUE_CLASS.get(item.itemtype.name, "nothing")

    query = DB_SESSION.query(klass)\
        .filter(klass.item_id == item.id)

    if start_time:
        query = query.filter(
            klass.timestamp > start_time)

    if end_time:
        query = query.filter(
            klass.timestamp < end_time)

    values = query.order_by(klass.timestamp.asc()).all()

    return values


def get_alerts(item, active=True, inactive=False):
    """Query Alerts."""
    alert_klass = ALERT_CLASS.get(item.itemtype.name)
    alerts = []
    triggers = get_triggers(item)

    for trigger in triggers:
        active_alert = DB_SESSION.query(alert_klass)\
            .filter(alert_klass.trigger_id == trigger.id)\
            .filter(alert_klass.end_time is None)

        alerts.extend(active_alert)

    return alerts


def get_itemname_by_name(name):
    item_name = DB_SESSION.query(ItemName)\
        .filter(ItemName.name == name)\
        .first()

    return item_name


def create_itemname(name, description):
    item_name = ItemName(name=name, description=description)
    DB_SESSION.add(item_name)
    return item_name


def get_itemcategory_by_name(name):
    cat = DB_SESSION.query(ItemCategory)\
        .filter(ItemCategory.name == name).first()
    return cat


def create_itemcategory(name):
    cat = ItemCategory(name=name)
    DB_SESSION.add(cat)
    return cat


def get_itemtype_by_name(name):
    item_type = DB_SESSION.query(ItemType)\
        .filter(ItemType.name == name).first()
    return item_type
