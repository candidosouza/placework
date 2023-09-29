const mix = require('laravel-mix');

mix.js(['', ''], '')
    .sass('', '')
    .copyDirectory('', '');

mix.setPublicPath('');
mix.options({
    processCssUrls: false,
});

if (mix.inProduction()) {
    mix.version();
}
