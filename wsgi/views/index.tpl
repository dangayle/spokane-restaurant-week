%include shared/header.tpl

            <div class="row">
                <nav class="span23">
                    <ul class="nav nav-list">
                    %for r in restaurants:
                        <li><a href="/restaurants/{{r['permalink']}}">{{r['name']}}</a></li>
                    %end
                    </ul>
                </nav>
                <section class="span10">
                    <p>Pick a restaurant from the left</p>
                </section>
            </div>
        </section>
    </body>
</html>