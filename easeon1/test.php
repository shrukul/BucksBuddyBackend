<?php
$url = 'https://test.payu.in/_payment';
$text="ABKDf0L8|5393401|25|test|Shrukul|shrukul99@gmail.com|||||||||||Hcj9jvpxMU";
$data = array('key' => 'ABKDf0L8', 'salt' => 'Hcj9jvpxMU', 'firstname' => 'Shrukul', 'email' => 'shrukul99@gmail.com', 'txnid' => '5393401', 'cvv' => '123', 'expiry' => 'May 2017', 'surl' => 'mainpage.html', 'amount' => '25', 'phone' => '8904890754', 'hash' =>  hash('sha512', $text), 'productinfo' => 'test   ', 'service_provider' => 'payu_paisa', 'surl' => 'mainpage.html');

// use key 'http' even if you send the request to https://...
$options = array(
    'http' => array(
        'header'  => "Content-type: application/x-www-form-urlencoded\r\n",
        'method'  => 'POST',
        'content' => http_build_query($data),
    ),
);
$context  = stream_context_create($options);
$result = file_get_contents($url, false, $context);
if ($result === FALSE) { /* Handle error */ }

var_dump($result);    
?>
