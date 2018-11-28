# WichtelMat

Flask server zum erstellen von Wichtelbeziehungen

## Nutzung

#### Wichtel-spiel erstellen:
`POST: at /create`
with payload:
```json
{
  "names": ["Peter", "James", "Kai", "Berd", "Holly"],
  "not_allowed": {
    "Peter": ["James"],
    "Berd": ["Holly"]
  }
}
```


#### Wichtel user abfragen:
`GET: at /game_id/user`

Beispiel: /4487891103134594895f558dbcb55787/Peter

## Libs
`pip3 install flask-restful`
