# Development

Install the following requirements in a virtualenv.
```
pip install -r requirements.txt
```

Run the server locally.
```
python builder.py
```

Compile the less manually using...
```
npm install -g less@1.3
lessc static/less/style.less static/css/style.css;
```

Then visit at [127.0.0.1:8000](http://127.0.0.1:8000)

# Deployment

To generate the site files, run...

```
python builder.py build
```

To deploy to S3, run...
```
python builder.py deploy
```

When prompted enter `www.cameronmaske.com`
