<script>
import {afterUpdate} from 'svelte';
let body;
export let user_id;
export let messages = [];

afterUpdate(() => {
    console.log('current user id', user_id)
    console.log('scroll Hight', body.scrollHeight)
    body.scrollTo(0, body.scrollHeight)
    body.focus()
})

</script>

<div id='chat-log' class='overflow-auto' bind:this={body}>

    {#each messages as msg}
        <div class="m-4">
            {#if msg.user_id != user_id}            
                <p class='text-xs ml-2 text-gray-600'>{msg.username}</p>
            {/if}
            <div class="flex {msg.user_id == user_id ? 'flex-row-reverse' : ''}">
                <p class="w-auto {msg.user_id == user_id ? 'bg-blue-600 text-gray-200' : 'bg-gray-400'} p-2 rounded-lg">{msg.body}</p>
            </div>
        </div>
    {/each}

</div>

<style>
	#chat-log{
		height: 90%;
	}

</style>