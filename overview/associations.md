---
description: Usage & configuration of associations
---

# 🪝 Associations

***

### Association by message

{% hint style="info" %}
Associations allow a session author to associate an object - such as a phrase or a web link, with a specific trigger keyword. When other members send a message containing the keyword, Ether will message with the associated item.
{% endhint %}

{% hint style="info" %}
Creating and managing associations in message requires mentioning Ether in the message
{% endhint %}

{% hint style="info" %}
Ether can now reference (in AI response) from the associations by keyword. For example, if you have gifs under keyword 'welcome' in your associations, you may prompt your AI interaction to end every response with the keyword "welcome", the AI response will trigger the gif.
{% endhint %}

<details>

<summary>Associate an object with a keyword</summary>

_`@ether trigger >> object`_

Associates the trigger keyword with the object given

`[ trigger object ] >> [ associated object ]`

</details>

<details>

<summary>Delete an association &#x26; its objects</summary>

_`@ether trigger >>`_

Erases all of the associations with the trigger and the trigger itself

`[ trigger ] >>`

</details>

<details>

<summary>Add multiple objects to a trigger in a single message</summary>

_`@ether trigger >> object1, object2, object3`_

Objects saved in series using comma

`[ trigger ] >> [ object1 ] , [ object2 ] , [ object3 ]`

</details>

<details>

<summary>Change the trigger word of an association</summary>

_`@ether old_name >< new_name`_

Updates the trigger object as a form of renaming, retaining the objects associated

`[ old name ] >< [ new name ]`

</details>

<details>

<summary>Remove a specific object from an association</summary>

_`@ether trigger >>`_

In reply to the object you want to remove. Requires Ether to have had sent the object in context as a message, reply to the message containing the object

`in reply:`\
`[ trigger ] >>`

</details>

{% hint style="info" %}
Triggers for associations must be a single word, numbers letters or symbols
{% endhint %}

{% hint style="info" %}
Chat sharing must be enabled for Ether to respond with associations when other users use keyword triggers
{% endhint %}

***

### Association by slash command

<details>

<summary>Manage associations</summary>

_`/association_options [ manage_associations ] [ option ]`_

Download, upload, view, or clear associations

Options:

* `download`
* `upload`
* `view`
* `clear`

_Example association .txt file:_

```
trigger1: object1, object2, object3
trigger2: object1, object2, object3
```

</details>

<details>

<summary>Add associations</summary>

_`/association_options [ add_association ] [ trigger >> object ]`_

Adding association by slash command is the same string style as adding by message, only the slash command replaces the need to mention the bot when creating an association

</details>

<details>

<summary>Share association creation</summary>

_`/association_options [ share_associations ] [ member mention ]`_

Share the ability for other members to create, remove, and rename associations in your session by message (shared association creation only works by message with bot mention)

</details>

{% hint style="info" %}
When downloading or uploading associations, Ether will send you the associations in direct message as a text file. When uploading associations, Ether will send a direct message and wait for you to supply a text file containing associations.
{% endhint %}

***
