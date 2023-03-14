import React from "react";
import { MDBCard, MDBCardBody, MDBCardTitle } from "mdb-react-ui-kit";
// import { Form } from "react";

const Name = () => {
  return (
    <div className="cam-selc-card">
      <MDBCard className="cam-selc-card">
        <MDBCardBody>
          <MDBCardTitle>Name</MDBCardTitle>

          {/* <Form>
          <Form.Control type="text" placeholder="Normal text" />
          </Form> */}
          <form >
            <label>
              
              <input type="text" />
            </label>
            {/* <input type="submit" value="Submit" /> */}
          </form>
        </MDBCardBody>
      </MDBCard>
    </div>
  );
};

export default Name;
