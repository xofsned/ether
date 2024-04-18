---
description: Extend a session into additional channels
---

# ⛓️ Extending Sessions

***

{% hint style="info" %}
Extending a session into another channel requires knowing the session number of the session you want to extend.
{% endhint %}

{% hint style="info" %}
A session's configuration cannot be altered inside a channel that is the extension of a session. Session configurations can only be altered in their source channel.
{% endhint %}

***

<details>

<summary>Extend</summary>

_`/manager [ extend ] [ session number ]`_

When invoked in a channel outside of an active session channel with a selected session number, the session is extended into the additional channel.

Logic:

* Invoked in a non-session channel with a session number creates the extension
* Invoked in an extended channel with the source session number removes the extension
* When invoking in an extended channel with a different source session number, the extension is migrated from one session to the other
* Session configurations can only be done in the source session channel, and not in extensions

</details>

{% hint style="info" %}
Use the session manager to view all sessions including their session numbers, or check the session configuration of a session for the session number.
{% endhint %}
