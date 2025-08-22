# Plugin Authoring

MakerWorks supports server and client plugins. Enable a plugin by adding its
name to the `PLUGINS` environment variable for the backend and `VITE_PLUGINS`
for the frontend.

Plugins expose a `setup()` function. See `makerworks/backend/tests/sample_plugin.py`
and `makerworks/frontend/src/plugins/samplePlugin.ts` for reference.
