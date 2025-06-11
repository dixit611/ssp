const { Server } = require("socket.io");
const io = new Server(5000, {
  cors: {
    origin: "*"
  }
});

io.on("connection", socket => {
  socket.on("join", room => {
    socket.join(room);
    socket.to(room).emit("joined");
  });

  socket.on("offer", (room, offer) => {
    socket.to(room).emit("offer", offer);
  });

  socket.on("answer", (room, answer) => {
    socket.to(room).emit("answer", answer);
  });

  socket.on("candidate", (room, candidate) => {
    socket.to(room).emit("candidate", candidate);
  });
});
