# Profile sync client
The profile sync client automatically synchronises users from a local identity store to a Pleio subsite. The client is built in Python and uses a REST/JSON API to connect to Pleio.

## How does it work?
The client is installed on a server that is maintained by the subsite holder. The client reads a local file (CSV) that contains a list users. It synchronises the state of the Pleio subsite with the local file. Users that are not on the site are added, the profile of existing users is updated and users not on the list are optionally banned.

The client uses two attributes to link local users with users on the subsite: **external_id** and **email**.

The profile sync client can be used together with Single Sign On (SSO) through SAML2. The SSO flow and the creation of a Pleio user is managed by [account.pleio.nl](https://account.pleio.nl). The authorisation of the Pleio user on the subsite is handled by the profile sync client.

The profile sync client outputs logs to standard output, but also writes the logs to the REST API. The logs can be inspected by the subsite administrator.

## Features
- Automatically creating, updating and blocking users from a subsite
- Ability to sync profile fields and site-specific avatars
- Test the synchronization with the dry-run option
- Remote log inspection by uploading the logs to the REST API

## Requirements
The package requires a Python version >= 3.3.

## Installation
Installation (and updates) are done with a single command:

    pip3 install pleio-profile-sync-client

## Usage
Use the CLI tool as follows:

```bash
    $ pleio-profile-sync-client --source example/users.csv --destination http://www.pleio.test:7000/profile_sync_api/
```

The CSV accepts the following fields:

- **external_id**, attribute to link local users with users on the subsite (optional)
- **name**, the fullname of the user
- **email**, the e-mailaddress of the user
- **avatar**, a relative link to the avatar in jpeg of the user
- **profile.\***, a field containing profile information, for example: `profile.occupation`.

Check [example/users.csv](./example/users.csv) for an example.
