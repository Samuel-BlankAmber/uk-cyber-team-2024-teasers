**Execution - 50 Points**

Summary: It's Handlebars SSTI

An `exe` titled `c2.exe` is provided which launches a locally-hosted web server. Dreamscape autoplays every time you move your cursor, caused by this very annoying script:
```js
document.addEventListener("mousemove", () => { document.querySelector("audio").play()});
```

There's several links on the page, the majority of which point to external sources.

The most significant of which is a `/book` endpoint, featuring a guestbook that allows you to leave comments.

There is also the following footnote on the main page:
```
Powered by Handlebars 4.7.8, 2004 release.
```

[Handlebars](https://handlebarsjs.com/) is a template engine. 2004 release is a red flag, as it could potentially indicate that it contains known CVEs.

However, Handlebars 4.7.8 is the latest release, and there are *no known vulnerabilities* (I don't know why it says 2004).

From analysing the network traffic (Inspect Element -> Network), commenting on the guestbook works by sending a POST request to the `/comment` endpoint.

The payload for this is Form data which contains two properties: a name and a comment.

The first thing to try is [SSTI](https://book.hacktricks.xyz/pentesting-web/ssti-server-side-template-injection) so let's try the classic `{{7*7}}` in the comment (the name also works).

```
Error: Parse error on line 1:
{{7*7}}
--^
Expecting 'ID', 'STRING', 'NUMBER', 'BOOLEAN', 'UNDEFINED', 'NULL', 'DATA', got 'INVALID'
```

Great sign. Let's try something more Handlebars-specific now: `{{this}}`

```
[object Object]
```

Seems like we've successfully used SSTI to steal some object, but we can't actually see its contents.

Handlebars features a number of [built-in helpers](https://handlebarsjs.com/guide/builtin-helpers.html) which allow you to add more complex functionality. One noteworthy helper is `log`.

Try the following payload: `{{log this}}`

The comment is blank, but in the console where the `exe` was run we can see a lot of output. We can see that the internal keys being referenced by the existing template are `poster`, `visited`, and `comment`. We can also see that we have access to an object called `global` - this is key.

The key-values stored within `this` are the context that is provided to Handlebars. We can prove this by entering `{{visited}}`. See how the visited date gets duplicated into the comments?

It's important to note that other global objects exist within JavaScript that may not be visible when logging `global`. For example, `global.process`.

I discovered this by reading writeups for Handlebars. A tip for this is to Google `site:ctftime.org: handlebars`

[This writeup in particular was helpful](https://ctftime.org/writeup/27816).
```
env can be accessed using global.process.env
```

So let's try this payload: `{{log global.process}}`

Envs (Environment Variables) are often used to store secrets, so this is a pretty good guess for where the flag could be.

If we scroll through the logs, we can see that we have found the flag!

So the final payload is 🥁🥁🥁 `{{global.process.env.FLAG}}`

```
Flag: R1d1ng_Th3_H4ndl3b4rs_0f_Expl0it4ti0n
```

Solve script:
```py
import requests

payload = "{{global.process.env.FLAG}}"
res = requests.post("http://localhost:3060/comment", data={"name": payload, "comment": " "})
print(res.text.split("Flag: ")[1].split("</div>")[0])
```
