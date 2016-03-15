<?php


	echo	 '<form id=msform name=myform action=http://easeon.pe.hu/index.php method=post onsubmit=return(validate());>';

		

	echo '<fieldset>';
	echo '<h3 class=fs-title>credit money</h3>';
	echo '<input type=text name=sender_id placeholder=SenderID />';
	echo '<span id=error background=red></span>';
	echo	'<input type=text name=amount placeholder=Amount />';
	echo	'<input type=submit name=next class=action-button value=Credit  />';
	echo '<span id=error1></span>';
	echo '</fieldset>';
	echo	'</form>';
?>
<script>
hide(document.getElementById("hide-slider"));
		  function hide (elements) {
  elements = elements.length ? elements : [elements];
  for (var index = 0; index < elements.length; index++) {
    elements[index].style.display = 'none';
  }
</script>