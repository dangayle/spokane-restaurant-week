<!doctype html>
<html>
    <head>
        <meta charset=utf-8>
        <meta name=description content="">
        <meta name=viewport content="width=device-width, initial-scale=1">
        <title>Untitled</title>
        <link rel=stylesheet href="css/style.css">
        <link rel=author href="humans.txt">
    </head>
    <body>
        <h1>Spokane Restaurant Week</h1>
        <ul>
        %for r in restaurants:
        <li><a href="/restaurants/{{r['permalink']}}">{{r['name']}}</a></li>
        %end
        </ul>
    </body>
</html>