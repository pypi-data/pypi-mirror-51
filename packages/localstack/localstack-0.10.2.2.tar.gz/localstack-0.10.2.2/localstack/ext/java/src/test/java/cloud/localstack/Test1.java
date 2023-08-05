package cloud.localstack;

import com.amazonaws.client.builder.AwsClientBuilder;
import com.amazonaws.services.s3.AmazonS3Client;
import com.amazonaws.services.s3.AmazonS3ClientBuilder;
import org.junit.Test;

import java.io.File;

import static org.junit.Assert.assertNotNull;

public class Test1 {

    final static AwsClientBuilder.EndpointConfiguration S3_ENDPOINT_CONFIGURATION
            = new AwsClientBuilder.EndpointConfiguration(
                    "http://localhost:4572", "us-east-1");

    // This method throws an error
    @Test
    public void testS3localstack() {

        final AmazonS3Client s3client = (AmazonS3Client) AmazonS3ClientBuilder.standard()
                .withEndpointConfiguration(S3_ENDPOINT_CONFIGURATION)
                .withPathStyleAccessEnabled(true)
                .build();

        s3client.createBucket("my-bucket-euayayyyaya");

        s3client.putObject("my-bucket-euayayyyaya", "my-password",
                new File("/etc/passwd"));

        assertNotNull(s3client);
    }

    //This method works without any problems
//    @Test
//    public void tests3aws() {
//
//        final AmazonS3Client s3client = (AmazonS3Client) AmazonS3ClientBuilder.standard()
//                .withRegion("us-west-2")
//                .build();
//
//        s3client.createBucket("my-bucket-euayayyyaya");
//
//        s3client.putObject("my-bucket-euayayyyaya", "my-password",
//                new File("/etc/passwd"));
//        assertNotNull(s3client);
//    }

}