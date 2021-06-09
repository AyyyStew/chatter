const login = (username, password) =>{
	let params = new URLSearchParams({
		username,
		password,
	})

	console.log(params)

	fetch("/auth/login", {
		body: params,
		headers: {
		  Accept: "application/json",
		  "Content-Type": "application/x-www-form-urlencoded"
		},
		method: "POST"
	})
	.then(response => {
		// if the response is not 200, log an error and return
		if (!response.ok){
			const status = response.status
			const message = response.statusText
			throw {status , message}
		}

		return response.json()
	})
	.then(data => {
		console.log('Success:', data);
		sessionStorage.setItem("CHATTER_TOKEN", data.access_token)
		window.location.replace("home.html")
	})
	.catch((error) => {
		console.error('Error:', error);
	});
}

loginForm = document.getElementById("login-form")
loginForm.addEventListener("submit", (e) =>{
	e.preventDefault()
	requestBody = {}
	for (element of loginForm.querySelectorAll("input")){
		requestBody[element.id] = element.value
	}
	
	login(requestBody["username"], requestBody["password"])

})
