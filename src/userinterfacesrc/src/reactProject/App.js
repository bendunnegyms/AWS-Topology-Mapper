import React from 'react';
import axios from 'axios';

class App extends React.Component {

  state = {
    ec2_details: [],
    name: "",
    description: "",
    id: "",
  }

  componentDidMount() {

    let data;

    axios.get('http://localhost:8000/wel/')
      .then(res => {
        data = res.data;
        this.setState({
          ec2_details: data
        });
      })
      .catch(err => { })
  }

  handleInput = (e) => {
    console.log("something is happening")
    this.setState({
      [e.target.name]: e.target.value,
    });
  };

  handleSubmit = (e) => {
    e.preventDefault();

    axios
      .post("http://localhost:8000/wel/", {
        name: this.state.name,
        description: this.state.description,
        security_group_id: this.state.id,
      })
      .then((res) => {
        this.setState({
          name: "",
          description: "",
          id: "",
        });
      })
      .catch((err) => { });
  };
  render() {
    return (

      <div>
        <form onSubmit={this.handleSubmit}>
          <div>
            <div>
              <span>
                Instance Name
                  </span>
            </div>
            <textarea
              placeholder="Instance Name"
              value={this.state.name} name="name"
              onChange={this.handleInput} />
          </div>

          <div>
            <div>
              <span>
                Description
                  </span>
            </div>
            <textarea
              placeholder="Instance Description"
              value={this.state.description} name="description"
              onChange={this.handleInput} />
          </div>

          <div>
            <div>
              <span>
                Security Group ID
                  </span>
            </div>
            <textarea
            placeholder="Security Group ID"
              value={this.state.id} name="id"
              onChange={this.handleInput} />
          </div>

          <button type="submit">
            Submit
          </button>
        </form>

        <hr
          style={{
            color: "#000000",
            backgroundColor: "#000000",
            height: 0.5,
            borderColor: "#000000",
          }}
        />

        {this.state.ec2_details.map((ec2_details, id) => (
          <div key={id}>
            <div>
              <div>Instance {id + 1}</div>
              <div>
                <blockquote>
                  <h1> {ec2_details.name} </h1>
                  <footer>
                    <cite>Instance Description: {ec2_details.description}</cite>
                    <br/>
                    <cite>Security Group: {ec2_details.security_group_id}</cite>
                  </footer>
                </blockquote>
              </div>
            </div>
            <span></span>
          </div>
        ))}
      </div>
    );
  }
}

export default App;