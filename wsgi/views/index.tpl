%include shared/header.tpl

        <ul>
        %for r in restaurants:
            <li><a href="/restaurants/{{r['permalink']}}">{{r['name']}}</a></li>
        %end
        </ul>


        </section>
    </body>
</html>