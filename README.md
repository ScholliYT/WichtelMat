# WichtelMat

Flask server zum erstellen von Wichtelbeziehungen

## Nutzung

#### Wichtel-spiel erstellen:
`POST: at /create`
with payload:
```json
{
	"host_url": "http://SAMPLE.PROVIDER.COM/",
	"names": ["Olaf", "Jan", "Udo", "Peter"],
	"not_allowed": {
		"Olaf": ["Udo"],
		"Peter": ["Olaf", "Jan"]
	}
}
```


#### Wichtel user abfragen:
`GET: at /game_id/users_random_number`

Beispiel: /4487891103134594895f558dbcb55787/9bc08e46afe1b6662716ecb75c08fa76995a9ce4ee13095bf16ffb1bec484a71

## Libs
`pip3 install flask-restful`
