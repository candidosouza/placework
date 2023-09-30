const mix = require('laravel-mix');

mix.sass('./placework/resources/styles/main.scss', './placework/static/css')
    .ts('./placework/resources/scripts/main.ts', './placework/static/js');
    // .js('./placework/static/js/main.js', './placework/static/js');
    // .copyDirectory('', '');

mix.setPublicPath('');
mix.options({
    processCssUrls: false,
});

if (mix.inProduction()) {
    mix.version();
}
