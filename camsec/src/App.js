

import React from "react";
import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import Navbar from './Components/Navbar';
import Homepage from './Components/Homepage';
// import Camerasetting from './Components/Camsetting/Camerasetting';
import Camerasetting from "./Components/Camsetting/Camerasetting"
import Adduser from './Components/Adduser/Adduser';
import AddImage from "./Components/Adduser/AddImage"
import Areaselection from './Components/AreaSelection/Areaselection';
import Eventoccur from './Components/EventOccurance/Eventoccur';
import LoginPage from './Components/LoginPage/LoginPage';
import Alertnotifs from './Components/Alertnotifs/Alertnotifs';
// import Eventoccur1 from './Components/AllNodelData/EventOccurance1/Eventoccur1';
import Eventoccur1 from "./Components/AllModelData/EventOccurance1/Eventoccur1";
import {
  BrowserRouter as Router,
  Switch,
  Route,
  Link
} from "react-router-dom";
//import LoginPage from "./Components/LoginPage/LoginPage";
export default function App() {
  return (
    <Router>
      <div>
        <Switch>
          <Route exact path="/">
            <LoginPage />
            </Route>
            <Route exact path="/home">
            <Homepage />
            <Navbar/>
           </Route>
           <Route exact path="/addimage">
            <AddImage />
            <Navbar/>
           </Route>
           
           <Route  path="/Camerasetting">
            <Camerasetting />
            <Navbar/>
          </Route>
          <Route path="/Adduser">
           <Navbar/>
            <Adduser />
          </Route>
          <Route path="/Eventoccur">
            <Navbar/>
            <Eventoccur /> 
          </Route>
          <Route path="/Eventoccur1">
            <Navbar/>
            <Eventoccur1 /> 
          </Route>
          <Route path="/Areaselection">
            <Navbar/>
            <Areaselection /> 
          </Route>  
        </Switch>
      </div>
    </Router>
  );
}

