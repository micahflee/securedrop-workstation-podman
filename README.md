# SecureDrop Workstation Podman

This repo is an attempt at getting [SecureDrop Workstation](https://github.com/freedomofpress/securedrop-workstation) (the SecureDrop client along with all of the associated components) to get running in containers with Podman rather than Qubes.

## Getting started

You'll need a valid `config.json` to connect to a SecureDrop server.

To generate one using a development server, follow [these instructions](https://developers.securedrop.org/en/latest/setup_development.html) and then start it like this:

```sh
cd securedrop
make dev-tor
```

After it boots, the `config.json` will appear in the output. It should look something like this:

```json
{
  "submission_key_fpr": "65A1B5FF195B56353CC63DFFCC40EF1228271441",
  "hidserv": {
    "hostname": "qqby5qwsupkwdstrhpqwpzm4zrrdiu56xg7xktjckvogoq4pskory2qd.onion",
    "key": "JAMNFZUVMKSAUX6E3SHNH2AKC7BUE45TUNWOEPYQ6SED3KH7TRIA"
  },
  "environment": "prod",
  "vmsizes": {
     "sd_app": 10,
     "sd_log": 5
  }
}
```

Copy this and save it to `config.json` in this folder.
