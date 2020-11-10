console.log('Sanity check!');
console.log(document.cookie);

function getCookie(name) {
	const value = `; ${document.cookie}`;
	const parts = value.split(`; ${name}=`);
	if (parts.length === 2) return parts.pop().split(';').shift();
}

fetch('/api/config/')
	.then((result) => {
		return result.json();
	})
	.then((data) => {
		// Initialize Stripe.js
		const stripe = Stripe(data.publicKey);

		// new
		// Event handler
		document.querySelector('#submitBtn').addEventListener('click', () => {
			fetch('http://127.0.0.1:8000/api/place-order/', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
					'X-CSRFToken': getCookie('csrftoken'),
				},
				body: JSON.stringify({
					products: [
						{
							product_id: 1,
							qty: 1,
						},
						{
							product_id: 2,
							qty: 3,
						},
					],
					address: {
						address_line1: 'Times Square',
						address_line2: 'Satya Castle,Shanti Nagar',
						state: 'Andhra Pradesh',
						city: 'Visakhapatnam',
						country: 'India',
						pincode: '530009',
					},
					success_url: 'http://localhost:8000/',
					cancelled_url: 'http://localhost:8000/',
				}),
			})
				.then((result) => {
					return result.json();
				})
				.then((data) => {
					console.log(data);
					return stripe.redirectToCheckout({
						sessionId: data.session_id,
					});
				})
				.then((res) => {
					console.log('No res');
					console.log(res);
				});
		});
	});
