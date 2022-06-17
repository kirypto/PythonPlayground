# Chat Server

This chat server is a more complicated usage of multiprocessing and multi-threading in python. The `chat_app.py` script
can be launched either in `server` or `client` mode and will either launch a chat server process or attempt to connect
to an existing one respectively.

The server process listens for incoming connections on a certain port, gathers 2 _(so they can chat with each other)_,
and creates a handler to pass messages back and forth between the 2 clients. It looks something like this:

**Server Process**
```mermaid
stateDiagram-v2

CloseServer: Shutdown (main thread)
ClientListener: Client Connection Listener (new process)
state ServerStartupFork <<fork>>

[*] --> ServerStartupFork
ServerStartupFork --> CloseServer
ServerStartupFork --> ClientListener: create client listener

state CloseServer {
    StopServer: terminate client \n listener process
    [*] --> StopServer: any key pressed
    StopServer --> [*]
}

state ClientListener {
    Conn1Listener: Listen for C1
    Conn2Listener: Listen for C2
    state CreateHandlerFork <<fork>>
    ChatRoomHandler: Chat Room Handler (new thread)
    
    [*] --> Conn1Listener
    Conn1Listener --> Conn2Listener: incoming connection
    Conn2Listener --> CreateHandlerFork: incoming connection
    CreateHandlerFork --> Conn1Listener: continue listening
    CreateHandlerFork --> ChatRoomHandler: create chat room handler for C1 & C2 
    
    state ChatRoomHandler {
        NameExchange: Exchange user names
        C1Msg: C1 Sending Message
        C2Msg: C2 Sending Message
        
        [*] --> NameExchange
        NameExchange --> C1Msg
        C1Msg --> C2Msg: Recieve C1's msg\nForward to C2
        C2Msg --> C1Msg: Recieve C2's msg\nForward to C1
    }
}

state ServerShutdownJoin <<join>>
CloseServer --> ServerShutdownJoin
ClientListener --> ServerShutdownJoin: on process terminated
ServerShutdownJoin --> [*]
```

---

The following will run the `chat_app.py` demo ***in server mode***. _(the `Set-Item` command at the beginning adds the project
root to the python path so that the following script can be run from this current directory)_
```shell
Set-Item -Path Env:PYTHONPATH -Value ($Env:PYTHONPATH + ";" + ((Get-Item .).parent.parent.parent.FullName) + ";");

python chat_app.py server
```

The following will run the `chat_app.py` demo ***in client mode***. _(the `Set-Item` command at the beginning adds the project
root to the python path so that the following script can be run from this current directory)_
```shell
Set-Item -Path Env:PYTHONPATH -Value ($Env:PYTHONPATH + ";" + ((Get-Item .).parent.parent.parent.FullName) + ";");

python chat_app.py client
```
