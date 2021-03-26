<script>
	import Chatbox from './Chatbox.svelte'

	const socket = new WebSocket('ws://localhost:5000');

	// Connection opened
	socket.addEventListener('open', function (event) {
		console.log('Connected to the WS Server!', event)
		let new_username = prompt("Please Enter Your name")
		socket.send(JSON.stringify({
			reg_user: true,
			new_username: new_username,
		}))
	});

	// Connection closed
	socket.addEventListener('close', function (event) {
		console.log('Disconnected from the WS Server!', event)
	});

	// Listen for messages
	socket.addEventListener('message', function (event) {
		console.log("recieved socket", event.data)
		let data = JSON.parse(event.data)

		// for registering the current user name
		if (data.reg_success){
			user_obj.id = data.user_id
			user_obj.username = data.username
			console.log("client registered", user_obj.id, user_obj.username)
			socket.send( JSON.stringify({
				add_user: true,
				username: user_obj.username,
				user_id: user_obj.id,
			}) )
		}

		if (data.users_list){
			users = data.users_list
			console.log("Updating the users list", users)
		}

		if (data.msg){
			console.log("Recieving Message")
			updateMsgs(data.msg)
		}

	});

	// Send a msg to the websocket
	const sendMsg = () => {
		// creating the new messsage
		let new_msg = {
			msg: {
				user_id: user_obj.id,
				username: user_obj.username,
				body: msg_input,
			}
		}
		socket.send(JSON.stringify(new_msg));
		// reseting the input field
		msg_input = ""
	}

	//adding it to the messages view & updating it
	const updateMsgs = (msg) => {
		messages.push(msg)
		messages = messages
		console.log(messages)
	}

	const handle_keydown = (e) => {
		if (e.key == "Enter") sendMsg()
	}

	let users= [];
	let msg_input = "";
	let user_obj = {
		id: 0,
		username: ""
	}
	let messages = [
		// {
		// 	user_id: 3,
		// 	username: 'Mike',
		// 	body: "just get it over with"
		// }
	];
</script>

<main class="flex">
	<div id="users-column" class="bg-blue-400 m-0 flex flex-col pt-16">
		{#each users as user}
			<p class="py-4 text-lg font-semibold mx-auto">{user.username}</p>
		{/each}
	</div>
	<div id="chat-body" class="bg-gray-200">
		<Chatbox messages={messages} user_id={user_obj.id}/>

		<div id="chat-message" class="bg-gray-700 flex p-3">
			<input type="text" bind:value={msg_input} on:keydown={handle_keydown} placeholder="Your message..." class="rounded-l-lg p-4 w-10/12 outline-none">
			<button on:click={sendMsg} class="bg-gray-400 p-2 w-24 rounded-r-lg focus:outline-white">Send</button>
		</div>
	</div>
</main>

<style>
	#users-column{
		width: 25vw;
		height: 100vh;
	}

	#chat-body{
		width: 75vw;
		height: 100vh;
	}

	#chat-message{
		width: 100%;
		height: 10%;
	}
</style>