%include shared/header.tpl

                <nav class="threecol">
                    <ul>
                    %for r in restaurants:
                        <li><a href="/restaurants/{{r['permalink']}}">{{r['name']}}</a></li>
                    %end
                    </ul>
                </nav>
                <section class="ninecol last">
                    <p>Pick a restaurant from the left</p>
                </section>
            </section>
        </div><!-- end container -->
    </body>
</html>