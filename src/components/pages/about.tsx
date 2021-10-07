import React from "react";
import Logo1 from "../../assets/img_1.jpeg";
import Logo2 from "../../assets/img_2.jpeg";
import Logo3 from "../../assets/img_3.jpeg";

const about = () => {
  return (
    <div className="front__info">
      <div className="front__info--container">
        <div className="front__info--container__left">
          <div className="front__info--container__left--heading">
            What are this parts?
          </div>
          <div className="front__info--container__left--para">
            A wardrobe full of different NFT sets of lidz, kix and shoes
            designed by FKB team which you can stake here and get your exclusive
            avatar out of it.
          </div>
          <div className="front__info--container__left--heading">Features</div>
          <div className="front__info--container__left--para">
            You can stake the parts into this platform and you will be provided
            an avatar made up of this parts which you can trade.
            <br /> V2 of this gear will be also be out shortly after the avatar
            release.
          </div>
        </div>
        <div className="front__info--container__right">
          <div>
            <img className="info-img" src={Logo1} alt="logo-1" />
          </div>
          <div>
            <img className="info-img" src={Logo2} alt="logo-2" />
            <img className="info-img" src={Logo3} alt="logo-3" />
          </div>
        </div>
      </div>
    </div>
  );
};

export default about;
