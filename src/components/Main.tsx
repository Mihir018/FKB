import React from "react";
import Header from "./pages/header";
import MintToken from "./pages/mintToken";
import About from "./pages/about";
import "./style.css";

const Main = () => {
  return (
    <div className="front">
      <Header />
      <MintToken />
      <About />
    </div>
  );
};

export default Main;
