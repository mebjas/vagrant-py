<?php
// Vagrant py client in php
namespace vagrantPYD;

define('IN_PIPE_LENGTH', 20);
define('OUT_PIPE_DIR', '../tmp/');
define('OUT_PIPE_NAME', 'pipe');
define('IN_PIPE_DIR', OUT_PIPE_DIR);
define('PIPE_INPUT_MAX_SIZE', 4096);
define('VPYDC_TIMEOUT', 600);

/**
 * Function to generata a random string of specified length.
 * @param int $len
 * @return String
 */
function randstr($len = 32)
{
    return vagrantClient::randStr($len);
}

class vagrantClient {

	// Time in seconds before which the method should do everything and
	// send back response, default = 10 minutes
	private $timeout;

	private $timeStarted;

	// Format of response to be sent back to calling script
	private $response = array(
			'error' => false,
			'timeout' => false,
			'data' => null
		);

	private $suffix;
	private $prefix;
	private $command;

	/**
	 * Constructor
	 * @param string: command to be sent, example: create <xml file path>
	 * @return array: information with format of $this->response. With extra data 
	 * as recieved from vagrant-pyd
	 */
	function __construct($timeout = -1) {
		$this->prefix = self::randStr(IN_PIPE_LENGTH);
		if ($timeout > 0) $this->timeout = $timeout;
		else $this->timeout = VPYDC_TIMEOUT;
	}

	// Function to do main pipe command send and wait for response
	private function work() {
		$this->command = $this->prefix ." "
				. $this->command ." "
				. $this->suffix ." ";

		$this->timeStarted = time();

		// Connect to the out pipe and send data to it!
		$handle = fopen(OUT_PIPE_DIR .OUT_PIPE_NAME, "w");
		fwrite($handle, $this->command);
		fclose($handle);

		$handle = fopen(IN_PIPE_DIR .$this->prefix, "r");
		while (true) {
			$return = fread($handle, PIPE_INPUT_MAX_SIZE);
			$return = json_decode($return, true);
			$return['time_taken'] = time() - $this->timeStarted;

			// Kill the pipe
			fclose($handle);
			unlink(IN_PIPE_DIR .$this->prefix);
			return $return;
		}
	}


	// Function to create a box based on @param:$path sent.
	// @param: path (str) the path of dir, which contains challenge.xml and files
	public function CreateBox($path) {
		$this->command = "create";
		$this->suffix = $path;
		return $this->work();
	}

	// Function to start a box
	// @param: boxID, the id of the box which you need to start
	public function StartChallenge($boxID) {
		$this->command = "start";
		$this->suffix = $boxID;
		return $this->work();
	}

	// Function to stop a box
	// @param: boxID, the id of the box which you need to stop
	public function StopChallenge($boxID) {
		$this->command = "stop";
		$this->suffix = $boxID;
		return $this->work();
	}

	// Function to destroy all running challenges
	public function destroyAll() {
		$this->command = "destroy all";
		$this->suffix = "";
		return $this->work();
	}

	// Function to get info on one or all boxes
	// @param: boxID, the id of box you need info about
	// else, just leave empty to get info about all
	public function infoBox($boxID = false) {
		if ($boxID) {
			$this->command = "info box";
			$this->suffix = $boxID;
		} else {
			$this->command = "info all box";
			$this->suffix = "";
		}
		return $this->work();
	}

	// Function to get info on one or all challenges
	// @param: challengeID, the id of challenge you need info about
	// else, just leave empty to get info about all
	public function infoChallenge($challengeID = false) {
		if ($challengeID) {
			$this->command = "info challenge";
			$this->suffix = $challengeID;
		} else {
			$this->command = "info all challenge";
			$this->suffix = "";
		}
		return $this->work();
	}

	/**
     * To generate a random string of specified length.
     * @param int $Length
     * @return String
     */
    public static function randStr($length = 32) {
        // Use `openssl_random_psuedo_bytes` if available; PHP5 >= 5.3.0
        if (function_exists("openssl_random_pseudo_bytes"))
            return substr(bin2hex(openssl_random_pseudo_bytes($length)), 0, $length);

        // Fall back to `mcrypt_create_iv`; PHP4, PHP5
        if (function_exists('mcrypt_create_iv')) 
            return substr(bin2hex(mcrypt_create_iv($length, MCRYPT_DEV_URANDOM)), 0, $length);

        $sha = '';
        $rnd = '';
        for ($i = 0; $i < $length; $i++) {
            $sha = hash('sha256', $sha.mt_rand());
            $char = mt_rand(0,62);
            $rnd .= $sha[$char];
        }

        return $rnd;
    }
};
