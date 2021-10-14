import React from "react";
import Linktree from "../../assets/linktree-logo.png";
import Twitter from "../../assets/twitter-logo.png";
import Telegram from "../../assets/telegram-logo.png";

const footer = () => {
  return (
    <div className="footer">
      <div className="footer__container">
        <div className="footer__container--title">Reach out to us at</div>
        <div className="footer__container--img-container">
          <a href="https://linktr.ee/FKB_Productions" target="_">
            <img className="social-img" src={Linktree} alt="linktr.ee logo" />
          </a>
          <a href="https://twitter.com/FKB_Productions" target="_">
            <img className="social-img" src={Twitter} alt="twitter logo" />
          </a>
          <a href="https://t.me/FKB_DCR" target="_">
            <img className="social-img" src={Telegram} alt="telegram logo" />
          </a>
        </div>
      </div>
    </div>
  );
};

export default footer;
