import React from "react";
import Header from "./pages/header";
import MintToken from "./pages/mintToken";
import About from "./pages/about";
import Info from "./pages/info";
import Footer from "./pages/footer";
import "./style.css";

const Main = () => {
  return (
    <>
      <div className="front">
        <Header />
        <MintToken />
        <About />
        <Info />
      </div>
      <Footer />
    </>
  );
};

export default Main;
