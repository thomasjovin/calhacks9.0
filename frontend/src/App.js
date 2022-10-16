import React, { useState, useEffect } from 'react';
import io from 'socket.io-client';

const socket = io("localhost:5000/", {
  transports: ["websocket"],
  cors: {
    origin: "http://localhost:3000/",
  },
});

function App() {
  const [isConnected, setIsConnected] = useState(socket.connected);
  const [lastPong, setLastPong] = useState(null);
  const [socketInstance, setSocketInstance] = useState("");

  useEffect(() => {
    socket.on('connect', () => {
      console.log('connected')
      setIsConnected(true);
    });

    socket.on('disconnect', () => {
      setIsConnected(false);
    });

    socket.on('pong', () => {
      setLastPong(new Date().toISOString());
    });
    
    setSocketInstance(socket);

      socket.on("connect", (data) => {
        console.log(data);
      });

      socket.on("disconnect", (data) => {
        console.log(data);
      });

      return function cleanup() {
        socket.disconnect();
      };
    // }

    // return () => {
    //   socket.off('connect');
    //   socket.off('disconnect');
    //   socket.off('pong');
    // };
  }, []);

  const sendPing = () => {
    socket.emit('ping', {'test':123});
  }

  return (
    <div>
      <p>Connected: { '' + isConnected }</p>
      <p>Last pong: { lastPong || '-' }</p>
      <button onClick={ sendPing }>Send ping</button>
    </div>
  );
}

export default App;