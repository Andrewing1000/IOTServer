const BASE_URL = "localhost:8080"; // Cambia por tu URL real
const SOCKET_URL = `ws://${BASE_URL}/ws/socket-server/`;

let socket = null;

export const setupSocket = () => {
  if (!socket || socket.readyState === WebSocket.CLOSED) {
    socket = new WebSocket(SOCKET_URL);

    // Eventos básicos
    socket.onopen = () => {
      console.log("WebSocket conectado");
    };

    socket.onclose = () => {
      console.warn("WebSocket desconectado");
      // Opcional: reconexión automática
      setTimeout(() => {
        console.log("Intentando reconectar...");
        setupSocket();
      }, 3000);
    };

    socket.onerror = (error) => {
      console.error("Error en WebSocket:", error);
    };
  }
  return socket;
};
