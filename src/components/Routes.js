import React, {Component} from 'react';
import { Container, Row, Col, Media} from 'reactstrap';
import './RoutesMap.css'

class Routes extends Component {

    createRouteCard = ({image, name, summary, maxElev, lat, lng}) => (
        <Col xs="12">
            <Media data-img_link={image} data-name={name} data-maxelev={maxElev} 
            data-lat={lat} data-lng={lng} onClick={this.props.handleRouteSelect} className="mb-4 route-card rounded p-1">
                <Media left>
                    <Media object src={image} className="route-small-image" />
                </Media>
                <Media body className="pl-3">
                    <Media heading>{name}</Media>
                    {summary}
                </Media>
            </Media>
        </Col>
    )

    render() {
        if (this.props.trails!==null) {
            if (this.props.trails!=='500') {
                return (
                    <Container>
                        <Row>
                            {this.props.trails.map(this.createRouteCard)}
                        </Row>
                    </Container>
                );
            }
            else {
                alert("Can't find location");
            }
        }
        else {
            return (
                <></>
            );
        }
    }
}

export default Routes;
