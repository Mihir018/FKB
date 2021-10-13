import React from "react";
import Logo1 from "../../assets/img_1.jpeg";
import Logo2 from "../../assets/img_2.jpeg";
import Logo3 from "../../assets/img_3.jpeg";

const about = () => {
  return (
    <div className="front__about">
      <div className="front__about--container">
        <div className="front__about--container__left">
          <div className="front__about--container__left--heading">
            What is FKB Gear?
          </div>
          <div className="front__about--container__left--para">
            A wardrobe full of different NFT's designed by FKB! Lidz, Kix, and
            Skinz will be available for staking and will change the appearance
            of your Fuckboy!
          </div>
          <div className="front__about--container__left--heading">Features</div>
          <div className="front__about--container__left--para">
            You will be able to stake and unstake the different FKB Gear on your
            Fuckboy within this platform. Get a matching set and change the
            character completely or unlock a hidden accessory! V2 of the FKB
            gear will be available shortly after Fuckboy launch!
          </div>
        </div>
        <div className="front__about--container__right">
          <div>
            <img className="about-img" src={Logo1} alt="logo-1" />
          </div>
          <div>
            <img className="about-img" src={Logo2} alt="logo-2" />
            <img className="about-img" src={Logo3} alt="logo-3" />
          </div>
        </div>
      </div>
    </div>
  );
};

export default about;
