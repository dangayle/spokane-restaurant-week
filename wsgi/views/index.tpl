%include shared/header.tpl
        <section class="wrap">
            <div class="row">
                <nav class="d25">
                    <ul>
                    %for r in restaurants:
                        <li><a href="/restaurants/{{r['permalink']}}">{{r['name']}}</a></li>
                    %end
                    </ul>
                </nav>
                <section class="d75">
                    <p>Pick a restaurant from the left</p>
                </section>
            </div>
        </section>
    </body>
</html>