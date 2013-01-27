%include shared/header.tpl

            <div class="row">
                <nav class="span3">
                    <div class="well sidebar-nav">
                        <ul class="nav nav-list">
                        %for r in restaurants:
                            <li><a href="/restaurants/{{r['permalink']}}">{{r['name']}}</a></li>
                        %end
                        </ul>
                    </div>
                </nav>
                <section class="span9">
                    <p>Pick a restaurant from the left</p>
                </section>
            </div>
        </section>
    </body>
</html>