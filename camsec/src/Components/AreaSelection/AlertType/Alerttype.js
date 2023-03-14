import React from "react";
import { MDBCard, MDBCardBody, MDBCardTitle } from "mdb-react-ui-kit";
import Alertdropdown from "./Alertdropdown";

import { useState } from "react";

const Alerttype = () => {
  const [selected, setSelected] = useState("Choose One");

  return (
    <div className="cam-selc-card" >
      <MDBCard className='cam-selc-card' >
        <MDBCardBody>
          <MDBCardTitle>Alert Type</MDBCardTitle>

          <Alertdropdown selected={selected} setSelected={setSelected} />  
          
        </MDBCardBody>
      </MDBCard>
    </div>
  );
};

export default Alerttype;
