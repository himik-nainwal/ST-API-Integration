import React from "react";
import { MDBCard, MDBCardBody, MDBCardTitle } from "mdb-react-ui-kit";
import Authoritydropdown from "./Ad";

import { useState } from "react";

const Authority = () => {
  const [selected, setSelected] = useState("Choose One");

  return (
    <div className="cam-selc-card" >
      <MDBCard className='cam-selc-card' >
        <MDBCardBody>
          <MDBCardTitle  style={{marginBottom:'19px',marginTop:'20px',fontSize:'15px'}}>Authority</MDBCardTitle>
          <Authoritydropdown selected={selected} setSelected={setSelected} />  
        </MDBCardBody>
      </MDBCard>
    </div>
  );
};

export default Authority;
