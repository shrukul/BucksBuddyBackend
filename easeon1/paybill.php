<?php

	echo	 '<form id=msform name=myform action=http://easeon.pe.hu/index.php method=post onsubmit=return(validate());>';

		

	echo '<fieldset>';
	echo '<h3 class=fs-title>pay bill </h3>';
	echo '<input type=text name=sender_id placeholder=Sender Id />';
	echo '<span id=error ></span>';
	echo	'<input type=text name=receiver_id placeholder=Receiver Id />';
	echo '<span id=error5 ></span>';
	echo	'<input type=password name=sender_pin placeholder=SenderPin />';
	echo '<span id=error4 ></span>';
	echo	'<input type=password name=receiver_pin placeholder=ReceiverPin />';
	echo '<span id=error3 ></span>';
	echo	'<input type=text name=amount placeholder=Amount />';
	echo '<span id=error1 ></span>';
	echo	'<input type=submit name=next class=action-button value=Pay  />';
	echo '</fieldset>';
	echo	'</form>';









?>