import asyncio
import websockets, json

class ServerSocket():
    def __init__(self, port=5000):
        self.connected = []
        self.port = port
        self.start_server = websockets.serve(self.server, "localhost", self.port)
        print(f'server started on port {port}')

        asyncio.get_event_loop().run_until_complete(self.start_server)
        asyncio.get_event_loop().run_forever()


    async def server(self, websocket, path):
        print('get new client', websocket)
        registered = False

        try:
            async for message in websocket:
                print('sending message', self.connected)
                msg_dict = json.loads(message)

                # === registering new user ===
                if msg_dict.get('reg_user') and not registered:
                    username = msg_dict['new_username']
                    user_id = len(self.connected) + 1
                    self.connected.append({
                        'socket': websocket,
                        'username': username,
                        'user_id': user_id
                    })
                    await websocket.send( json.dumps({
                        'reg_success': True,
                        'username': username,
                        'user_id': user_id
                    }) )
                    registered = True
                    print(f"New user registered => id={user_id}: username={username}")
                    continue

                for conn in self.connected:
                    
                    if msg_dict.get('add_user') or msg_dict.get('remove_user'):
                        print('current connected', self.connected)
                        users_list = self.get_users_list()
                        await conn['socket'].send( json.dumps({
                            'users_list': users_list
                        }))

                    else:
                        # sending message for all users
                        await conn['socket'].send(message)
                        print("message sent", message)

        finally:
            # === Unregister user ===
            print("remove client", self.connected[user_id-1])
            del self.connected[user_id-1]
            for conn in self.connected:
                if conn != websocket:
                    users_list = self.get_users_list()
                    await conn['socket'].send( json.dumps({
                        'users_list': users_list
                    }))


    def get_users_list(self):
        users_list = list( map(lambda x: {
            'user_id': x['user_id'],
            'username': x['username']
        }, self.connected))

        return users_list

server = ServerSocket()