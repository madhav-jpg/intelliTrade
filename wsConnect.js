// var axios = require('axios');
// var data = JSON.stringify({
//     "mode": "FULL",
//     "exchangeTokens": {
//         "NSE": ["17957"]
//     }
// });

// var config = {
//   method: 'post',
//   url: 'https://apiconnect.angelbroking.com/rest/secure/angelbroking/market/v1/quote/',
//   headers: { 
//     'X-PrivateKey': 'BZrjesgR', 
//     'Accept': 'application/json, application/json', 
//     'X-SourceID': 'WEB, WEB', 
//     'X-ClientLocalIP': 'CLIENT_LOCAL_IP', 
//     'X-ClientPublicIP': 'CLIENT_PUBLIC_IP', 
//     'X-MACAddress': 'MAC_ADDRESS', 
//     'X-UserType': 'USER', 
//     'Authorization': 'Bearer eyJhbGciOiJIUzUxMiJ9.eyJ1c2VybmFtZSI6Iks1MjY0ODg2MSIsInJvbGVzIjowLCJ1c2VydHlwZSI6IlVTRVIiLCJ0b2tlbiI6ImV5SmhiR2NpT2lKSVV6VXhNaUlzSW5SNWNDSTZJa3BYVkNKOS5leUp6ZFdJaU9pSkxOVEkyTkRnNE5qRWlMQ0psZUhBaU9qRTNNVE00TURFM05Ua3NJbWxoZENJNk1UY3hNemN3TkRVNE9Dd2lhblJwSWpvaVpHRmxaV05tT1dFdE1XRTNOUzAwT1RJM0xUa3pabUV0Tm1OaFpXRTFORFppTkRRMElpd2liMjF1WlcxaGJtRm5aWEpwWkNJNk9Dd2ljMjkxY21ObGFXUWlPaUl6SWl3aWRYTmxjbDkwZVhCbElqb2lZMnhwWlc1MElpd2lkRzlyWlc1ZmRIbHdaU0k2SW5SeVlXUmxYMkZqWTJWemMxOTBiMnRsYmlJc0ltZHRYMmxrSWpvNExDSnpiM1Z5WTJVaU9pSXpJaXdpWkdWMmFXTmxYMmxrSWpvaVlqbGlNMlJsTkRJdE9ERTJNaTB6T1dZMUxUazRNelF0TWpVNVl6UmhPV013T1RFMUlpd2lZV04wSWpwN2ZYMC5YYmNMWWltXzJzeHozejgxN3NCazFJY2ZBTXZreHotTHhMVTRBYzY4ZkVBcHBGY2pZa3h5amotUnc0NXlqVWdUYXcyVDN5QVZ2S1lLVE0yMWdHV0w5USIsIkFQSS1LRVkiOiJCWnJqZXNnUiIsImlhdCI6MTcxMzcwNDY0OCwiZXhwIjoxNzEzODAxNzU5fQ.XYJEpEAASgk6x_OT5lzvTjpgJ1yAMxRVZQoHRfoCLFuKHTWPfdc3-SysfkuOjpN2jxySef4TMDr09nLafXNpVg', 
//     'Content-Type': 'application/json'
//   },
//   data : data
// };

// axios(config)
// .then(function (response) {
//   console.log(JSON.stringify(response.data));
// })
// .catch(function (error) {
//   console.log(error);
// });
let WebSocketV2 = require('smartapi-javascript');

let web_socket = new WebSocketV2({
	jwttoken: 'Bearer eyJhbGciOiJIUzUxMiJ9.eyJ1c2VybmFtZSI6Iks1MjY0ODg2MSIsInJvbGVzIjowLCJ1c2VydHlwZSI6IlVTRVIiLCJ0b2tlbiI6ImV5SmhiR2NpT2lKSVV6VXhNaUlzSW5SNWNDSTZJa3BYVkNKOS5leUp6ZFdJaU9pSkxOVEkyTkRnNE5qRWlMQ0psZUhBaU9qRTNNVE01TnpjeE1EVXNJbWxoZENJNk1UY3hNemc0TURVd01Td2lhblJwSWpvaU56VXhNbVkxTWpRdE16a3hPUzAwTkdRNUxXSTVaall0TURaa05qTTBObUV5WXpBNElpd2liMjF1WlcxaGJtRm5aWEpwWkNJNk9Dd2ljMjkxY21ObGFXUWlPaUl6SWl3aWRYTmxjbDkwZVhCbElqb2lZMnhwWlc1MElpd2lkRzlyWlc1ZmRIbHdaU0k2SW5SeVlXUmxYMkZqWTJWemMxOTBiMnRsYmlJc0ltZHRYMmxrSWpvNExDSnpiM1Z5WTJVaU9pSXpJaXdpWkdWMmFXTmxYMmxrSWpvaVlqbGlNMlJsTkRJdE9ERTJNaTB6T1dZMUxUazRNelF0TWpVNVl6UmhPV013T1RFMUlpd2lZV04wSWpwN2ZYMC5VVFpuM3hGYTdFLU9ETF9TeFMzUXVQMjM1UVg5aTN3eTJKS0ctQWFRTzhPQ1dBUVN5RnQxaVd2NTVRdHo4azAzVkJ6cEJ5bEJRQVRQSTlpbGUwS1JGUSIsIkFQSS1LRVkiOiJCWnJqZXNnUiIsImlhdCI6MTcxMzg4MDU2MSwiZXhwIjoxNzEzOTc3MTA1fQ.xWPqrVFW7uJbjGTJ_gTz9fWoealvSQYiXYNAYWv2UXxoRG7bnW57u1os_-uS8ZqIVIQlxy9USrSSWKqsnBfzKw',
	apikey: 'BZrjesgR',
	clientcode: 'K52648861',
	feedtype: 'order_feed',
});

web_socket.connect().then((res) => {
	let json_req = {
		correlationID: 'abcde12345',
		action: 1,
		params: {
			mode: 3,
			tokenList: [
				{
					exchangeType: 1,
					tokens: ['17957'],
				},
			],
		},
	};

	web_socket.fetchData(json_req);
	web_socket.on('tick', receiveTick);

	function receiveTick(data) {
		console.log('receiveTick:::::', data);
	}
});