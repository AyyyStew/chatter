// check if a token exists in session storage.
// if it doens't send user back to the login screen 
const redirectIfNoToken = ()=>{
	const token = sessionStorage.getItem("CHATTER_TOKEN")

	if (token === null){
		window.location.replace("index.html")
	}
}
redirectIfNoToken()



chatSocket = new WebSocket(`ws:/${location.host}/api/chat?token=${sessionStorage.getItem("CHATTER_TOKEN")}`)
chatSocket.addEventListener('message', (event) => {
	jsondata = JSON.parse(event.data)
	console.log(jsondata)
	
	globalChat = document.getElementById("global-chat")

	renderComment(globalChat, jsondata.message, jsondata.user.username, jsondata.timestamp)
	
})

sendButton = document.getElementById("global-chat").querySelector(".chat-textbox-send")
sendButton.addEventListener("click", ()=>{

})


const renderComment = (chatroom, text, username, timestamp) => {
	let currentUser = sessionStorage.getItem("CHATTER_USERNAME")
	
	// this couples the css and js. its probably a bad idea
	let newComment = document.createElement("div")
	newComment.classList.add("comment")
	if (jsondata.user.username == username){
		newComment.classList.add("comment-from-me")
	}
	
	let user = document.createElement("p")
	user.appendChild(document.createTextNode(username))
	user.classList.add("comment-user")

	let commentText = document.createElement("p")
	// create text node instead of innerhtml so no html or js injection
	// i got a feeling that is gonna bite me in the butt later
	commentText.appendChild(document.createTextNode(text))
	commentText.classList.add("comment-text")
	
	newComment.appendChild(user)
	newComment.appendChild(commentText)

	globalChat.querySelector(".comments").appendChild(newComment)
}
