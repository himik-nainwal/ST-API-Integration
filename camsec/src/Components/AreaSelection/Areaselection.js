import React from "react";
import 'bootstrap/dist/css/bootstrap.min.css';
// import Camsdropdown from "./Camselection/Camsdropdown";
import Camselection from "../Camsetting/Cameraselection";
import Points from "./Points/Points";
import Alerttype from "./AlertType/Alerttype";

const Areaselection = () => {
  return (
    <div className="area">
      <div className="home">
        <div className="head">
          <div className="heading">
            <div className="head1">HEALTHCARE SEC</div>
            <div className="head2">CAMSEC.AI</div>
          </div>
        </div>

        <hr id="hr"/>
      </div>

      <div className="area-panel">
            <div className="selection-set">
                <div className="select-cam"><Camselection /></div>
                <div className="points"><Points /> </div>
                <div className="alert-type"><Alerttype /></div>
                <div className="area-submit">
                  <button id="ar-submit" >Submit</button>
                </div>
            </div>
            <div className="selected-cam"></div>
        </div>

        
    </div>

  );
};

export default Areaselection;
