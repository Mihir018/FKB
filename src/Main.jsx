import React from "react";
import { BrowserRouter, Route } from "react-router-dom";
import FrontPage from "./components/Main";

const Main = () => {
  return (
    <BrowserRouter>
      <Route path="/" component={FrontPage} />
    </BrowserRouter>
  );
};

export default Main;
