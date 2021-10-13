import React from "react";
import Logo from "../../assets/logo.jpeg";
import Gif from "../../assets/gif.gif";

const header = () => {
  return (
    <div className="front__header">
      <div className="front__header--typo">
        <div className="front__header--typo__heading">FKB Production</div>
        <div className="front__header--typo__sub-heading">
          Stake your official FKB Gear to change your Fuckboy!
        </div>
      </div>
      <div className="front__header--images">
        <div className="front__header-first">
          <div className="front__header--gif">
            <img src={Gif} alt="gif" className="gif" />
          </div>
        </div>
        <div className="front__header--second">
          <div className="front__header--logo">
            <img className="logo" src={Logo} alt="logo" />
          </div>
        </div>
      </div>
    </div>
  );
};

export default header;
