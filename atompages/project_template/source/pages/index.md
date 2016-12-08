title: Home


{% for page in statistics.sorted_by_date %}

{% if not page.hidden_link %}

<a href="{{page.link}}"><h2>{{page.title}}</h2></a>

{% if not "home" in page.link and not "impressum" in page.link %}

  <p>Written by {{page.author}} | {{page.ctime |datetimeformat('%d. %b. %Y')}}</p>
  <p>{{page.description}}</p>
  <hr>
  <br/>

{% endif %}

{% endif %}

{% endfor %}
