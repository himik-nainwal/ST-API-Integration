import React from "react";
import { MDBCard, MDBCardBody, MDBCardTitle } from "mdb-react-ui-kit";
// import { Form } from "react";

const Userid = () => {
  return (
    <div className="cam-selc-card">
      <MDBCard className="cam-selc-card">
        <MDBCardBody>
          <MDBCardTitle>ID No.</MDBCardTitle>

          {/* <Form>
          <Form.Control type="text" placeholder="Normal text" />
          </Form> */}
          <form >
            <label>
              
              <input type="user id" />
            </label>
            {/* <input type="submit" value="Submit" /> */}
          </form>
        </MDBCardBody>
      </MDBCard>
    </div>
  );
};

export default Userid;
