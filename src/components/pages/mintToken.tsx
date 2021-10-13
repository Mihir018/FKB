/* eslint-disable @typescript-eslint/no-unused-vars */
import React, { useState } from "react";
import ConnectButton from "../ConnectWallet";
import DisconnectButton from "../DisconnectWallet";
import { TezosToolkit } from "@taquito/taquito";

const MintToken = () => {
  const [Tezos, setTezos] = useState<TezosToolkit>(
    new TezosToolkit("https://api.tez.ie/rpc/granadanet")
  );
  const [contract, setContract] = useState<any>(undefined);
  const [publicToken, setPublicToken] = useState<string | null>("");
  const [wallet, setWallet] = useState<any>(null);
  const [userAddress, setUserAddress] = useState<string>("");
  const [userBalance, setUserBalance] = useState<number>(0);
  const [storage, setStorage] = useState<number>(0);
  const [copiedPublicToken, setCopiedPublicToken] = useState<boolean>(false);
  const [beaconConnection, setBeaconConnection] = useState<boolean>(false);
  const [activeTab, setActiveTab] = useState<string>("transfer");

  // Granadanet Increment/Decrement contract
  const contractAddress: string = "KT1K3XVNzsmur7VRgY8CAHPUENaErzzEpe4e";
  return (
    <div className="front__mint-token">
      <div>
        <div className="front__mint-token--typo">
          1337 Fuckboy characters will be available for minting! Rarity, hidden
          items, and character changes coming!!!
        </div>
        <ConnectButton
          Tezos={Tezos}
          setContract={setContract}
          setPublicToken={setPublicToken}
          setWallet={setWallet}
          setUserAddress={setUserAddress}
          setUserBalance={setUserBalance}
          setStorage={setStorage}
          contractAddress={contractAddress}
          setBeaconConnection={setBeaconConnection}
          wallet={wallet}
        />
        <div className="front__mint-token__btn">
          <div className="mint-btn">Mint</div>
        </div>
      </div>
    </div>
  );
};

export default MintToken;
