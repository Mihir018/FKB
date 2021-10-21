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
  } else {
    const fileName = multerReq.file.filename;
    await pinata
      .testAuthentication()
      .catch((err) => res.status(500).json(JSON.stringify(err)));
    const readableStreamForFile = fs.createReadStream(`./upoads/${fileName}`);
    const options = {
      pinataMetadata: {
        name: req.body.title.replace(/\s/g, "-"),
        keyvalues: {
          description: req.body.description,
        },
      },
    };
    const pinnedFile = await pinata.pinFileToIPFS(
      readableStreamForFile,
      options
    );
    if (pinnedFile.IpfsHash && pinnedFile.PinSize > 0) {
      fs.unlinkSync(`./uploads/${fileName}`);
      // pins metadata
      const metadata = {
        name: req.body.title,
        description: req.body.description,
        symbol: "TUT",
        artifactUri: `ipfs://${pinnedFile.IpfsHash}`,
        displayUri: `ipfs://${pinnedFile.IpfsHash}`,
        creators: [req.body.creator],
        decimals: 0,
        thumbnailUri: "https://tezostaquito.io/img/favicon.png",
        is_transferable: true,
        shouldPreferSymbol: false,
      };

      const pinnedMetadata = await pinata.pinJSONToIPFS(metadata, {
        pinataMetadata: {
          name: "TUT-metadata",
        },
      });

      if (pinnedMetadata.IpfsHash && pinnedMetadata.PinSize > 0) {
        res.status(200).json({
          status: true,
          msg: {
            imageHash: pinnedFile.IpfsHash,
            metadataHash: pinnedMetadata.IpfsHash,
          },
        });
      } else {
        res
          .status(500)
          .json({ status: false, msg: "metadata were not pinned" });
      }
    } else {
      res.status(500).json({ status: false, msg: "file was not pinned" });
    }
  }
});

app.listen(port, () =>
  console.log(`Server started on http://localhost:${port}`)
);
