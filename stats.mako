<%def name="funnel_print(funnel)">
  <li>${funnel.name}: ${funnel.count}</li>
  <ul>
  %for child in funnel.children:
    ${funnel_print(child)}
  %endfor
  </ul>
</%def>

<html>
<head>
   <title HeyZap Stats for ${today}</title>
</head>
<body>
  <h1>HeyZap Stats for ${today}</h1>
  <h2>Page Views</h2>
    <ul>
    %for name,count in counts.items():
      <li>${name}: ${count}</li>
    %endfor
    </ul>
  <h2>Funnels</h2>
    <ul>
    %for funnel in funnels:
      ${funnel_print(funnel)}
    %endfor
</body>
        
  
