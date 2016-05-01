var gulp = require('gulp');
var uglify = require('gulp-uglify');
var concat = require('gulp-concat');
var pump = require('pump');

gulp.task('default', function() {
  pump([
        gulp.src([
            'argux_server/static/js/source/argux.js',
            'argux_server/static/js/source/rest.js',
        ]),
        concat('argux.js'),
        gulp.dest('argux_server/static/js/debug')
    ]
    );
  pump([
        gulp.src('argux_server/static/js/debug/argux.js'),
        uglify(),
        gulp.dest('argux_server/static/js/')
    ]
    );
});
