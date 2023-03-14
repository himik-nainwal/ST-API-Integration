import React from "react";
import { MDBCard, MDBCardBody, MDBCardTitle } from "mdb-react-ui-kit";
import Authoritydropdown from "./Authoritydropdown";

import { useState } from "react";

const Authority = () => {
  const [selected, setSelected] = useState("Choose One");

  return (
    <div className="cam-selc-card" >
      <MDBCard className='cam-selc-card' >
        <MDBCardBody>
          <MDBCardTitle>Authority</MDBCardTitle>

          <Authoritydropdown selected={selected} setSelected={setSelected} />  
          
        </MDBCardBody>
      </MDBCard>
    </div>
  );
};

export default Authority;
