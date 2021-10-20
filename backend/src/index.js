import express from "express";
import cors from "cors";
import pinataSDK from "@pinata/sdk";
import fs from "fs";
import multer from "multer";
import dotenv from "dotenv";

dotenv.config();
const secretKey = process.env.SECRET_KEY;
const apiSecretKey = process.env.API_SECRET_KEY;
const port = process.env.NODE_ENV === "production" ? process.env.PORT : 9000;

const corsOptions = {
  origin: ["http://localhost:3000"],
  optionsSuccessStatus: 200,
};
const upload = multer({ dest: "uploads/" });
const app = express();
app.use(cors(corsOptions));
app.use(express.json({ limit: "50mb" }));
app.use(
  express.urlencoded({
    limit: "50mb",
    extended: true,
    parameterLimit: 5000,
  })
);

const pinata = pinataSDK(apiSecretKey, secretKey);

app.post("/mint", upload.single("image"), async (req, res) => {
  const multerReq = req;
  if (!multerReq.file) {
    res.status(500).json({ status: false, msg: "no file provided !!" });
  }
});

app.listen(port, () =>
  console.log(`Server started on http://localhost:${port}`)
);
